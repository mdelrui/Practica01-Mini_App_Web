import { describe, it, expect, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'

vi.mock('axios', () => ({
  default: {
    post: vi.fn(),
  },
}))

import axios from 'axios'
import App from '../App.vue'

describe('App', () => {
  it('renders the API summary when backend returns summary and main_ideas', async () => {
    vi.mocked(axios.post).mockResolvedValue({
      data: {
        summary: 'Resumen de prueba',
        main_ideas: ['Idea 1', 'Idea 2'],
      },
    })

    const wrapper = mount(App)

    const textarea = wrapper.find('textarea')
    await textarea.setValue('Texto de prueba para resumir')

    const submitButton = wrapper
      .findAll('button')
      .find((button) => button.text().includes('Resumir Texto'))

    expect(submitButton).toBeTruthy()
    await submitButton!.trigger('click')
    await flushPromises()

    expect(wrapper.text()).toContain('Resumen de prueba')
    expect(wrapper.text()).toContain('Idea 1')
  })
})
