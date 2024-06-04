// src/plugins/vuetify.js
import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import ko from 'vuetify/es5/locale/ko';

Vue.use(Vuetify);

const vuetify = new Vuetify({
  lang: {
    locales: { ko },
    current: 'ko',
  },
  theme: {
    themes: {
      light: {
        primary: '#3f51b5',
        secondary: '#b0bec5',
        accent: '#8c9eff',
        error: '#b71c1c',
      },
    },
  },
});

export default vuetify;
