import { beforeEach, describe, expect, it, vi } from 'vitest'
import { computed, reactive, shallowRef } from 'vue'
import { flushPromises, mount } from '@vue/test-utils'

vi.mock('axios', () => ({
  default: {
    post: vi.fn(),
    isAxiosError: (error: unknown) =>
      typeof error === 'object' && error !== null && 'isAxiosError' in error
        ? error.isAxiosError === true
        : false
  }
}))

const clerkMocks = vi.hoisted(() => ({
  auth: {},
  clerk: {}
}))

vi.mock('@clerk/vue', () => ({
  useAuth: () => clerkMocks.auth,
  useClerk: () => clerkMocks.clerk
}))

import axios from 'axios'
import App from '../App.vue'

const authState = reactive({
  loaded: true,
  signedIn: false,
  token: null as string | null
})
const getToken = vi.fn<() => Promise<string | null>>()
const openSignIn = vi.fn()
const signOut = vi.fn()

function configureClerk() {
  clerkMocks.auth = {
    isLoaded: computed(() => authState.loaded),
    isSignedIn: computed(() => authState.signedIn),
    getToken: computed(() => getToken)
  }
  clerkMocks.clerk = shallowRef({ openSignIn, signOut })
}

function mountConfiguredApp() {
  return mount(App, { props: { clerkConfigured: true } })
}

function makeAxiosError(status: number) {
  return Object.assign(new Error('request failed'), {
    isAxiosError: true,
    response: { status }
  })
}

describe('App authentication', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    authState.loaded = true
    authState.signedIn = false
    authState.token = null
    getToken.mockImplementation(async () => authState.token)
    signOut.mockImplementation(async () => {
      authState.signedIn = false
    })
    vi.mocked(axios.post).mockResolvedValue({
      data: { summary: 'Resumen de prueba', main_ideas: ['Idea 1'] }
    })
    configureClerk()
  })

  it('shows an explicit configuration error and blocks processing without a Clerk key', async () => {
    const wrapper = mount(App)
    await wrapper.get('textarea').setValue('Texto de prueba')

    expect(wrapper.get('[role="alert"]').text()).toContain('no está configurada')
    expect(wrapper.get('button[type="submit"]').attributes('disabled')).toBeDefined()
    await wrapper.get('form').trigger('submit')
    await flushPromises()

    expect(axios.post).not.toHaveBeenCalled()
  })

  it('shows loading state and prevents submissions until Clerk resolves', async () => {
    authState.loaded = false
    authState.signedIn = true
    const wrapper = mountConfiguredApp()
    await wrapper.get('textarea').setValue('Texto de prueba')

    expect(wrapper.get('[role="status"]').text()).toContain('Comprobando')
    expect(wrapper.get('button[type="submit"]').attributes('disabled')).toBeDefined()
    await wrapper.get('form').trigger('submit')
    await flushPromises()

    expect(axios.post).not.toHaveBeenCalled()
  })

  it('opens the sign-in modal in place while signed out', async () => {
    const wrapper = mountConfiguredApp()
    const pathBeforeOpening = window.location.pathname

    expect(wrapper.text()).toContain('Inicia sesión para resumir un texto.')
    const signInButton = wrapper
      .findAll('button')
      .find((button) => button.text().trim() === 'Iniciar sesión')!
    await signInButton.trigger('click')

    expect(openSignIn).toHaveBeenCalledOnce()
    expect(window.location.pathname).toBe(pathBeforeOpening)
    expect(axios.post).not.toHaveBeenCalled()
  })

  it('shows signed-in state and signs out without navigating', async () => {
    authState.signedIn = true
    const wrapper = mountConfiguredApp()
    const pathBeforeSignOut = window.location.pathname

    expect(wrapper.text()).toContain('Sesión iniciada')
    const signOutButton = wrapper
      .findAll('button')
      .find((button) => button.text().trim() === 'Cerrar sesión')!
    await signOutButton.trigger('click')
    await flushPromises()

    expect(signOut).toHaveBeenCalledOnce()
    expect(wrapper.text()).toContain('Inicia sesión para resumir un texto.')
    expect(window.location.pathname).toBe(pathBeforeSignOut)
  })

  it('sends the current Clerk token only as a bearer header with the existing JSON body', async () => {
    authState.signedIn = true
    authState.token = 'test-session-token'
    const wrapper = mountConfiguredApp()
    await wrapper.get('textarea').setValue('Texto de prueba')
    await wrapper.get('form').trigger('submit')
    await flushPromises()

    expect(getToken).toHaveBeenCalledOnce()
    expect(axios.post).toHaveBeenCalledWith(
      'http://127.0.0.1:8000/resumir',
      { text: 'Texto de prueba', main_ideas: false },
      { headers: { Authorization: 'Bearer test-session-token' } }
    )
    expect(JSON.stringify(vi.mocked(axios.post).mock.calls[0]?.[1])).not.toContain(
      'test-session-token'
    )
    expect(wrapper.text()).not.toContain('test-session-token')
    expect(wrapper.text()).toContain('Resumen de prueba')
  })

  it.each([
    [401, 'Tu sesión no es válida o ha caducado'],
    [503, 'No se pudo verificar la sesión temporalmente']
  ])(
    'shows a distinct %i response without clearing the text or retrying',
    async (status, message) => {
      authState.signedIn = true
      authState.token = 'test-session-token'
      vi.mocked(axios.post).mockRejectedValue(makeAxiosError(status))
      const wrapper = mountConfiguredApp()
      await wrapper.get('textarea').setValue('Texto que debe conservarse')
      await wrapper.get('form').trigger('submit')
      await flushPromises()

      expect(wrapper.text()).toContain(message)
      expect((wrapper.get('textarea').element as HTMLTextAreaElement).value).toBe(
        'Texto que debe conservarse'
      )
      expect(axios.post).toHaveBeenCalledOnce()
      expect(wrapper.text()).not.toContain('test-session-token')
      if (status === 401) {
        const reauthenticateButton = wrapper
          .findAll('button')
          .find((button) => button.text().trim() === 'Volver a iniciar sesión')
        expect(reauthenticateButton).toBeDefined()
        await reauthenticateButton!.trigger('click')
        expect(openSignIn).toHaveBeenCalledOnce()
      } else {
        expect(wrapper.text()).not.toContain('Volver a iniciar sesión')
      }
    }
  )

  it('does not send a request when token acquisition fails', async () => {
    authState.signedIn = true
    getToken.mockRejectedValue(new Error('token unavailable'))
    const wrapper = mountConfiguredApp()
    await wrapper.get('textarea').setValue('Texto que debe conservarse')
    await wrapper.get('form').trigger('submit')
    await flushPromises()

    expect(wrapper.text()).toContain('No se pudo obtener la sesión')
    expect((wrapper.get('textarea').element as HTMLTextAreaElement).value).toBe(
      'Texto que debe conservarse'
    )
    expect(axios.post).not.toHaveBeenCalled()
  })
})
