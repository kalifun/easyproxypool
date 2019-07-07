import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Regist from '@/components/Regist'
import Home from '@/components/Home/Index'
import userList from '@/components/Home/userList'
import ipList from '@/components/Home/ipList'
import adminList from '@/components/Home/adminList'
import addUser from '@/components/Home/addUser'
import about from '@/components/Home/about'


Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/regist',
      name: 'Regist',
      component: Regist
    },
    {
      path: '/home',
      name: 'Home',
      component: Home,
      children: [
        {
          path: '',
          component: ipList
        },
        {
          path: '/userList',
          component: userList,
          meta: ['数据管理', '用户列表'],
        },
        {
          path: '/ipList',
          component: ipList,
          meta: ['数据管理', '数据列表'],
        },
        {
          path: '/adminList',
          component: adminList,
          meta: ['数据管理', '管理员列表'],
        },
        {
          path: '/addUser',
          component: addUser,
          meta: ['添加数据','添加用户']
        },
        {
          path: '/about',
          component: about,
          meta: ['关于你']
        }
      ]
    }
  ]
});

router.beforeEach((to,from,next) => {
  if (to.path === '/' || to.path === '/regist') {
    next()
  } else {
    let token = localStorage.getItem('Authorization');
    if (token === 'null' || token === '' || token === null) {
      next('/');
    }else {
      next()
    }
  }
});

export default router
