import { beforeEach, describe, expect, it, vi } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'
import App from '../App.vue'
import { resumirTexto } from '../services/resumen'

vi.mock('../services/resumen', () => ({
  resumirTexto: vi.fn(),
}))

describe('Aplicación app1', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('muestra el título y el campo de texto', () => {
    const wrapper = mount(App)

    expect(wrapper.text()).toContain('RESUMIDOR AUTOMÁTICO')
    expect(wrapper.find('textarea').exists()).toBe(true)
  })

  it('desactiva el botón cuando no hay texto', () => {
    const wrapper = mount(App)
    const boton = wrapper.find('button[type="submit"]')

    expect(boton.attributes('disabled')).toBeDefined()
  })

  it('envía el texto y muestra el resumen recibido', async () => {
    vi.mocked(resumirTexto).mockResolvedValue('Resumen de prueba generado')

    const wrapper = mount(App)
    await wrapper.get('textarea').setValue('Texto de ejemplo para resumir')
    await wrapper.get('form').trigger('submit')
    await flushPromises()

    expect(resumirTexto).toHaveBeenCalledWith('Texto de ejemplo para resumir')
    expect(wrapper.text()).toContain('Resumen de prueba generado')
  })

  it('muestra un mensaje de error si falla la generación del resumen', async () => {
    vi.mocked(resumirTexto).mockRejectedValue(new Error('Fallo en backend'))

    const wrapper = mount(App)
    await wrapper.get('textarea').setValue('Texto de ejemplo')
    await wrapper.get('form').trigger('submit')
    await flushPromises()

    expect(wrapper.text()).toContain(
      'No se pudo generar el resumen. Comprueba la conexión e inténtalo de nuevo.',
    )
  })
})
