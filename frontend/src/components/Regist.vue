<template>
  <div class="regist">
    <el-row style="z-index: 1;height: 100%">
      <el-card class="regist-box">
        <h1>Regist</h1>
        <el-form :rules="rules" :model="Userform" ref="Userform"  status-icon>
          <el-form-item prop="username">
            <el-input placeholder="用户名" v-model.number="Userform.username"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input type="password" placeholder="密码" v-model="Userform.password"></el-input>
          </el-form-item>
          <el-form-item prop="checkpwd">
            <el-input type="password" placeholder="再次输入密码" v-model="Userform.checkpwd"></el-input>
          </el-form-item>
          <el-form-item style="text-align: center">
            <el-button type="primary" @click="submitForm('Userform')">注册</el-button>
            <el-button type="danger" @click="resetForm('Userform')">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-row>
  </div>
</template>

<script>
    export default {
        name: "Regist",
      data() {
        var checkaccount = (rule,value,callback) => {
          if (value === ''){
            callback(new Error("请输入用户名"))
          }else {
            if (Number.isInteger(value)) {
              callback(new Error('账号不能为数值'));
            }
            callback();
          }
        };
        var validatePass = (rule,value,callback) => {
          if (value === ''){
            callback(new Error("请输入密码"))
          }else {
            if (this.Userform.checkpwd !== ''){
              this.$refs.Userform.validateField('checkpwd');
            }
            callback();
          }
        };
        var validatePass2 = (rule,value,callback) => {
          if (value === ''){
            callback(new Error("请再次输入密码"))
          }else if (value !== this.Userform.password) {
            callback(new Error("密码不一致"))
          }else {
            callback();
          }
        };
        return {
          Userform: {
            username: '',
            password: '',
            checkpwd: ''
          },
          rules: {
            username: [
              {validator: checkaccount, trigger: 'blur'}
            ],
            password: [
              {validator: validatePass, trigger: 'blur'}
            ],
            checkpwd: [
              {validator: validatePass2, trigger: 'blur'}
            ]
          }
        }
      },
      methods: {
        resetForm(Userform) {
          this.$refs[Userform].resetFields();
        },
        submitForm(Userform) {
          this.$refs[Userform].validate((valid => {
            if (valid) {
                this.$http.post('/regist',{
                  username: this.Userform.username,
                  password: this.Userform.password,
                  password1: this.Userform.checkpwd
                }).then(res => {
                  this.$message({
                    message: '注册成功',
                    type: 'success'
                  });
                  this.$router.push('/')
                }).catch((error) => {
                  if (error.response.status === 401) {
                    let msg = error.response.data;
                    this.$message({
                      message: msg['message'],
                      type: 'info'
                    })
                  }else {
                    this.$message({
                      message: '请求失败',
                      type: 'info'
                    })
                  }
                })
            }
          }))
        }
      }
    }
</script>

<style scoped>
  .regist-box{
    width: 20%;
    top: 50%;
    left: 50%;
    position: absolute;
    padding: 10px 40px 10px 40px;
    transform: translate3d(-50%, 50%,0);
  }
  .regist-box h1{
    text-align: center;
  }
</style>
