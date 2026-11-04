import { beforeEach, describe, expect, it, vi } from 'vitest'
import { computed, reactive, shallowRef } from 'vue'
import { flushPromises, mount } from '@vue/test-utils'

vi.mock('axios', () => ({
  default: {
    post: vi.fn(),
    isAxiosError: (error: unknown) =>
      typeof error === 'object' && error !== null && 'isAxiosError' in error
        ? error.isAxiosError === true
        : false,
  },
}))

const clerkMocks = vi.hoisted(() => ({
  auth: {},
  clerk: {},
}))

vi.mock('@clerk/vue', () => ({
  useAuth: () => clerkMocks.auth,
  useClerk: () => clerkMocks.clerk,
  UserButton: {
    name: 'UserButton',
    render: () => null,
  },
}))

import axios from 'axios'
import App from '../App.vue'

const authState = reactive({
  loaded: true,
  signedIn: false,
  token: null as string | null,
})
const getToken = vi.fn<() => Promise<string | null>>()
const openSignIn = vi.fn()
const openSignUp = vi.fn()
const signOut = vi.fn()

function configureClerk() {
  clerkMocks.auth = {
    isLoaded: computed(() => authState.loaded),
    isSignedIn: computed(() => authState.signedIn),
    getToken: computed(() => getToken),
  }
  clerkMocks.clerk = shallowRef({ openSignIn, openSignUp, signOut })
}

function mountConfiguredApp() {
  return mount(App)
}

function makeAxiosError(status: number) {
  return Object.assign(new Error('request failed'), {
    isAxiosError: true,
    response: { status },
  })
}

describe('App summary flow', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    authState.loaded = true
    authState.signedIn = false
    authState.token = null
    getToken.mockImplementation(async () => authState.token)
    openSignIn.mockResolvedValue(undefined)
    openSignUp.mockResolvedValue(undefined)
    signOut.mockImplementation(async () => {
      authState.signedIn = false
    })
    vi.mocked(axios.post).mockResolvedValue({
      data: { summary: 'Resumen de prueba', mainIdeas: ['Idea 1'] },
    })
    configureClerk()
  })

  it('shows the sign-in and sign-up actions when the user is not authenticated', () => {
    const wrapper = mountConfiguredApp()

    expect(wrapper.text()).toContain('Iniciar sesión')
    expect(wrapper.text()).toContain('Crear cuenta')
    expect(wrapper.find('textarea').exists()).toBe(false)
  })

  it('keeps empty text disabled and enforces the configured text limit', async () => {
    authState.signedIn = true
    authState.token = 'test-session-token'

    const wrapper = mountConfiguredApp()
    const textarea = wrapper.get('textarea')
    const submitButton = wrapper.get('button[type="submit"]')

    expect(submitButton.attributes('disabled')).toBeDefined()
    expect(textarea.attributes('maxlength')).toBe('5000')

    await textarea.setValue('Texto válido')
    expect(submitButton.attributes('disabled')).toBeUndefined()
  })

  it('accepts only .txt and .md files and rejects other extensions', async () => {
    authState.signedIn = true
    authState.token = 'test-session-token'

    const wrapper = mountConfiguredApp()
    const textarea = wrapper.get('textarea')
    const dropZone = textarea.element.parentElement as HTMLElement

    const readDropEvent = (file: File) => {
      const event = new Event('drop', { bubbles: true })
      Object.defineProperty(event, 'dataTransfer', {
        value: { files: [file] },
        configurable: true,
      })
      return event
    }

    const txtFile = new File(['texto plano'], 'entrada.txt', { type: 'text/plain' })
    const mdFile = new File(['# Título'], 'entrada.md', { type: 'text/markdown' })
    const invalidFile = new File(['binario'], 'entrada.pdf', { type: 'application/pdf' })

    await dropZone.dispatchEvent(readDropEvent(txtFile))
    await flushPromises()
    await dropZone.dispatchEvent(readDropEvent(mdFile))
    await flushPromises()

    expect((textarea.element as HTMLTextAreaElement).value).toContain('Título')

    await dropZone.dispatchEvent(readDropEvent(invalidFile))
    await flushPromises()

    expect((textarea.element as HTMLTextAreaElement).value).toContain('Título')
  })

  it('sends the bearer token with the selected options and summary length when the form is submitted', async () => {
    authState.signedIn = true
    authState.token = 'test-session-token'
    vi.mocked(axios.post).mockResolvedValue({
      data: { summary: 'Resumen de prueba' },
    })

    const wrapper = mountConfiguredApp()
    await wrapper.get('textarea').setValue('Texto de prueba')

    const detailedButton = wrapper
      .findAll('button')
      .find((button) => button.text().trim() === 'Detallado')
    await detailedButton!.trigger('click')

    const switches = wrapper.findAll('button[role="switch"]')
    expect(switches).toHaveLength(2)
    await switches[0]!.trigger('click')
    await switches[1]!.trigger('click')

    await wrapper.get('form').trigger('submit')
    await flushPromises()

    expect(getToken).toHaveBeenCalledOnce()
    expect(axios.post).toHaveBeenCalledWith(
      'http://127.0.0.1:8000/resumir',
      {
        text: 'Texto de prueba',
        main_ideas: true,
        glossary: true,
        summary_length: 'detallado',
      },
      { headers: { Authorization: 'Bearer test-session-token' } },
    )
  })

  it('shows a user-facing authentication error for 401 and 503 responses', async () => {
    authState.signedIn = true
    authState.token = 'test-session-token'

    for (const [status, message] of [
      [401, 'Tu sesión no es válida o ha caducado'],
      [503, 'No se pudo verificar la sesión temporalmente'],
    ] as [number, string][]) {
      vi.mocked(axios.post).mockRejectedValue(makeAxiosError(status))

      const wrapper = mountConfiguredApp()
      await wrapper.get('textarea').setValue('Texto que debe conservarse')
      await wrapper.get('form').trigger('submit')
      await flushPromises()

      expect(wrapper.text()).toContain(message)
      expect((wrapper.get('textarea').element as HTMLTextAreaElement).value).toBe(
        'Texto que debe conservarse',
      )

      if (status === 401) {
        expect(wrapper.text()).toContain('Volver a iniciar sesión')
      }
    }
  })

  it('renders the result sections and supports copy plus local export', async () => {
    authState.signedIn = true
    authState.token = 'test-session-token'
    const writeText = vi.fn().mockResolvedValue(undefined)
    Object.defineProperty(navigator, 'clipboard', {
      value: { writeText },
      configurable: true,
    })

    const createObjectURL = vi.fn(() => 'blob:mock-url')
    const revokeObjectURL = vi.fn()
    vi.stubGlobal('URL', { createObjectURL, revokeObjectURL })

    vi.mocked(axios.post).mockResolvedValue({
      data: {
        summary: 'Resumen exportable',
        mainIdeas: ['Idea principal'],
        glossary: [{ concept: 'Concepto', definition: 'Definición' }],
      },
    })

    const wrapper = mountConfiguredApp()
    await wrapper.get('textarea').setValue('Texto de prueba')
    await wrapper.get('form').trigger('submit')
    await flushPromises()

    expect(wrapper.text()).toContain('RESUMEN')
    expect(wrapper.text()).toContain('IDEAS PRINCIPALES')
    expect(wrapper.text()).toContain('GLOSARIO')
    expect(wrapper.text()).toContain('Resumen exportable')

    const copyButtons = wrapper.findAll('button[aria-label="Copiar"]')
    expect(copyButtons).toHaveLength(3)
    await copyButtons[0]!.trigger('click')
    await copyButtons[1]!.trigger('click')
    await copyButtons[2]!.trigger('click')

    expect(writeText).toHaveBeenCalledTimes(3)
    expect(writeText).toHaveBeenNthCalledWith(1, 'RESUMEN\nResumen exportable')
    expect(writeText).toHaveBeenNthCalledWith(2, 'IDEAS PRINCIPALES\n1. Idea principal')
    expect(writeText).toHaveBeenNthCalledWith(3, 'GLOSARIO\n- Concepto: Definición')

    const txtButton = wrapper.findAll('button').find((button) => button.text().trim() === '.txt')
    const mdButton = wrapper.findAll('button').find((button) => button.text().trim() === '.md')

    await txtButton!.trigger('click')
    await mdButton!.trigger('click')

    expect(createObjectURL).toHaveBeenCalledTimes(2)
    expect(revokeObjectURL).toHaveBeenCalledTimes(2)
  })

  it('does not send empty or whitespace-only text', async () => {
    authState.signedIn = true
    authState.token = 'test-session-token'

    const wrapper = mountConfiguredApp()
    const textarea = wrapper.get('textarea')

    for (const value of ['', '   ', '\n\t  ']) {
      await textarea.setValue(value)
      await wrapper.get('form').trigger('submit')
      await flushPromises()

      expect(axios.post).not.toHaveBeenCalled()
    }

    expect(getToken).not.toHaveBeenCalled()
  })

  it('does not send the request when no session token is available', async () => {
    authState.signedIn = true
    getToken.mockResolvedValue(null)

    const wrapper = mountConfiguredApp()
    await wrapper.get('textarea').setValue('Texto de prueba')
    await wrapper.get('form').trigger('submit')
    await flushPromises()

    expect(getToken).toHaveBeenCalledOnce()
    expect(axios.post).not.toHaveBeenCalled()
  })

  it('renders only the summary when optional sections are absent', async () => {
    authState.signedIn = true
    authState.token = 'test-session-token'

    vi.mocked(axios.post).mockResolvedValue({
      data: { summary: 'Resumen sin secciones opcionales' },
    })

    const wrapper = mountConfiguredApp()
    await wrapper.get('textarea').setValue('Texto de prueba')
    await wrapper.get('form').trigger('submit')
    await flushPromises()

    expect(wrapper.text()).toContain('Resumen sin secciones opcionales')
    expect(wrapper.text()).not.toContain('IDEAS PRINCIPALES')
    expect(wrapper.text()).not.toContain('GLOSARIO')
  })
})
