import { describe, expect, it, vi } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'
import { nextTick } from 'vue'
import App from '../services/App.vue'
import { resumirTexto } from '../services/resumen'

vi.mock('../services/resumen', () => ({
  resumirTexto: vi.fn(),
}))

const resumirTextoMock = vi.mocked(resumirTexto)

describe('Aplicación', () => {
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

  it('activa el botón cuando escribimos texto', async () => {
    const wrapper = mount(App)

    await wrapper.find('textarea').setValue('Este es un texto de prueba')

    expect(wrapper.find('button[type="submit"]').attributes('disabled')).toBeUndefined()
  })

  it('muestra el número de palabras', async () => {
    const wrapper = mount(App)

    await wrapper.find('textarea').setValue('Hola mundo desde Vitest')

    expect(wrapper.text()).toContain('4 palabras')
  })

  it('borra el texto al pulsar el botón de borrar', async () => {
    const wrapper = mount(App)

    await wrapper.find('textarea').setValue('Texto que quiero borrar')
    await wrapper.find('button[aria-label="Borrar texto"]').trigger('click')

    expect((wrapper.find('textarea').element as HTMLTextAreaElement).value).toBe('')
  })

  it('muestra el resumen cuando la petición funciona', async () => {
    resumirTextoMock.mockResolvedValueOnce('Este es el resumen')
    const wrapper = mount(App)

    await wrapper.find('textarea').setValue('Un texto largo para resumir')
    await wrapper.find('form').trigger('submit')
    await flushPromises()
    await nextTick()

    expect(wrapper.text()).toContain('Este es el resumen')
    expect(resumirTextoMock).toHaveBeenCalledWith('Un texto largo para resumir')
  })

  it('muestra un mensaje cuando la petición falla', async () => {
    resumirTextoMock.mockRejectedValueOnce(new Error('Error de conexión'))
    const wrapper = mount(App)

    await wrapper.find('textarea').setValue('Texto para probar el error')
    await wrapper.find('form').trigger('submit')
    await flushPromises()
    await nextTick()

    expect(wrapper.text()).toContain('No se pudo generar el resumen')
  })
})
