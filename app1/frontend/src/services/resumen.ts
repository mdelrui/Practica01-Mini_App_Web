import axios from 'axios'

// Configuración básica del cliente HTTP con axios
// En Vercel se usa la ruta relativa del frontend; en local, Vite redirige las llamadas /api al backend
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  timeout: 35000,
})

// Función que envía el texto al backend y devuelve el resumen generado
export async function resumirTexto(texto: string): Promise<string> {
  const respuesta = await api.post('/api/resumir', { texto })
  return respuesta.data.resumen
}
