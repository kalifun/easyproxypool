<template>
    <div class="adduser">
      <top-header></top-header>
      <div class="userform">
        <el-form label-width="80px" :model="UserForm" :rules="rules" ref="UserForm" status-icon>
          <el-form-item label="用户名：" prop="username">
            <el-input v-model="UserForm.username"></el-input>
          </el-form-item>
          <el-form-item label="密码：" prop="password">
            <el-input type="password" v-model="UserForm.password"></el-input>
          </el-form-item>
<!--          <el-form-item label="权限">-->
<!--            <el-checkbox-group v-model="UserForm.permission">-->
<!--              <el-checkbox-button label="增" name="type"></el-checkbox-button>-->
<!--              <el-checkbox-button label="删" name="type"></el-checkbox-button>-->
<!--              <el-checkbox-button label="改" name="type"></el-checkbox-button>-->
<!--            </el-checkbox-group>-->
<!--          </el-form-item>-->
          <el-form-item label="角色">
            <el-radio-group v-model="UserForm.usertype"  size="medium">
              <el-radio border label="3">普通用户</el-radio>
              <el-radio border label="2">管理员</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item size="large">
            <el-button type="primary" @click="Createuser">立即创建</el-button>
            <el-button @click="ResetForm('UserForm')">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
</template>

<script>
    import TopHeader from "../../common/top-header";
    export default {
        name: "addUser",
        components: {TopHeader},
        data(){
          var checkusername = (rule,value,callback) => {
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
            UserForm: {
              username: '',
              password: '',
              // permission: [],
              usertype: '3',
            },
            rules: {
              username: [
                {validator: checkusername, trigger: 'blur'}
              ],
              password: [
                {validator: checkpassword, trigger: 'blur'}
              ]
            }
          }
        },
      methods: {
        Createuser(){
          this.$http.post('/adduser',{username:this.UserForm.username,password:this.UserForm.password,usertype:this.UserForm.usertype})
            .then(res => {
              this.$message({
                message: '创建成功',
                type: 'success'
              });
              if (this.UserForm.usertype === 3) {
                this.$router.push('/userList')
              } else {
                this.$router.push('/adminList')
              }
            }).catch(error =>{
              let msg = error.response.data['message'];
              let stat = error.response.status;
              if (stat === 401 || stat === 403) {
                this.$message({
                  message: msg,
                  type: 'info'
                });
              } else {
                this.$message({
                  message: '创建失败',
                  type: 'info'
                });
              }
          });
        },
        ResetForm(UserForm) {
          this.$refs[UserForm].resetFields();
        }
      }
    }
</script>

<style scoped>
.adduser{
  margin: 35px auto;
  width: 50%;
  }
.userform{
  margin: 35px auto;
  width: 50%;
}
</style>
