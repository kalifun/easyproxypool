import axios from 'axios'
import {Message} from "element-ui";
import router from '@/router/index'

axios.defaults.baseURL = 'http://127.0.0.1:5000';

axios.interceptors.request.use(
  config => {
    if (config.url==='/' || config.url === '/regist') {

    } else {
      if (localStorage.getItem('Authorization')) {
        config.headers.Authorization = localStorage.getItem('Authorization');
      }
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          localStorage.removeItem('Authorization');
          Message("认证失效");
          router.push('/')
      }
    }
    return Promise.reject(error)
  }
);

export default axios;
