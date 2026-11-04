/// <reference types="vite/client" />

declare module '@vue/eslint-config-typescript' {
  export function defineConfigWithVueTs(...configs: any[]): any

  export const vueTsConfigs: {
    recommended: any
  }
}

declare module 'eslint-plugin-vue' {
  const plugin: {
    configs: {
      'flat/essential': any[]
    }
  }

  export default plugin
}

declare module '@vitest/eslint-plugin' {
  const plugin: {
    configs: {
      recommended: any
    }
  }

  export default plugin
}

declare module 'eslint-plugin-oxlint' {
  const plugin: {
    buildFromOxlintConfigFile: (file: string) => any[]
  }

  export default plugin
}

declare module 'eslint-config-prettier/flat' {
  const skipFormatting: any
  export default skipFormatting
}

interface ImportMetaEnv {
  readonly VITE_CLERK_PUBLISHABLE_KEY?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
