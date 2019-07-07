<template>
  <div class="login">
    <el-row style="z-index: 1;height: 100%">
      <el-card class="login-box">
        <h1>Proxy Pool</h1>
        <el-form :model="LoginForm" :rules="rules" ref="LoginForm" status-icon>
          <el-form-item prop="account">
            <el-input placeholder="用户" v-model="LoginForm.account"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input  type="password" placeholder="密码" v-model="LoginForm.password"></el-input>
          </el-form-item>
          <el-form-item style="text-align:center">
            <el-button type="primary" @click="TryLogin('LoginForm')">登录</el-button>
            <el-button type="danger" @click="RestButton('LoginForm')">重置</el-button>
            <el-button type="info" @click="jumpregist">注册</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-row>
  </div>
</template>

<script>
    export default {
        name: "Login",
      data() {
        var checkaccount = (rule,value,callback) => {
          if (value === '') {
            callback(new Error("账号不能为空"))
          }
          callback();
        };
        var checkpassword = (rule,value,callback) => {
          if (value === '') {
            callback(new Error("密码不能为空"))
          }
          callback();
        };
        return {
          LoginForm: {
            account: '',
            password: ''
          },
          rules: {
            account: [
              {validator: checkaccount, trigger: 'blur'}
            ],
            password: [
              {validator: checkpassword, trigger: 'blur'}
            ]
          }
        }
      },
      methods: {
        RestButton(LoginForm) {
          this.$refs[LoginForm].resetFields();
        },
        TryLogin(LoginForm) {
          this.$refs[LoginForm].validate((valid => {
            if (valid) {
              this.$http.post('/login',{username:this.LoginForm.account,password:this.LoginForm.password})
                .then(res =>{
                  let auth = res.data['Authorization'];
                  this.$message({
                    message: "登录成功",
                    type: "success"
                  });
                  // this.changeLogin({Authorization: auth});
                  localStorage.setItem('Authorization',auth);
                  // console.log(localStorage.getItem('Authorization'))
                  this.$router.push('/home')
                }).catch(error => {
                  if (error.response.status === 401) {
                    let msg = error.response.data['message'];
                    this.$message({
                      'message': msg,
                      type: 'info'
                    })
                  } else {
                    this.$message({
                      message: "登录失败",
                      type: "info"
                    })
                  }
              });
            }
          }))
        },
        jumpregist() {
          this.$router.push('/regist')
        }
      }
    }
</script>

<style scoped>
  .login{
    background: url("../assets/2.jpg") no-repeat scroll center center / cover;
    background-size: 100% 100%;
    height: 100%;
    width: 100%;
    position: fixed;
  }
  .login-box{
    width: 20%;
    top: 50%;
    left: 50%;
    border: none;
    position: absolute;
    padding: 10px 40px 10px 40px;
    box-shadow: 0 0 25px #cac6c6;
    background: rgba(4, 22, 51, 0.69);
    transform: translate3d(-50%, -50%,0);
    -webkit-transform: translate3d(-50%, -50%,0);
  }
  .login-box h1 {
    text-align: center;
    color: #cac6c6;
  }
</style>
