import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

export default createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi },
  },

  theme: {
    defaultTheme: 'tarefas',
    themes: {
      tarefas: {
        dark: false,
        colors: {
          primary: '#5B4BE0',
          secondary: '#00B8A9',
          background: '#F4F5FB',
          surface: '#FFFFFF',
          error: '#D64550',
          success: '#2E9E5B',
        },
      },
    },
  },

  // Props padrão: aplicadas a toda instância do componente.
  // Evita repetir variant/density/rounded em cada tag.
  defaults: {
    VCard: { rounded: 'lg' },
    VBtn: { rounded: 'lg' },
    VTextField: { variant: 'outlined', density: 'comfortable' },
  },
})
