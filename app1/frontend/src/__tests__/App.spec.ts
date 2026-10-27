import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import App from '../App.vue'

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
})
