<template>
    <div class="adduser">
      <top-header></top-header>
      <div class="userform">
        <el-form label-width="80px" :model="UserForm">
          <el-form-item label="用户名：">
            <el-input v-model="UserForm.username"></el-input>
          </el-form-item>
          <el-form-item label="密码：" >
            <el-input v-model="UserForm.password"></el-input>
          </el-form-item>
          <el-form-item label="权限">
            <el-checkbox-group v-model="UserForm.permission">
              <el-checkbox-button label="增" name="type"></el-checkbox-button>
              <el-checkbox-button label="删" name="type"></el-checkbox-button>
              <el-checkbox-button label="改" name="type"></el-checkbox-button>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="角色">
            <el-radio-group v-model="UserForm.usertype"  size="medium">
              <el-radio border label="普通用户"></el-radio>
              <el-radio border label="管理员"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item size="large">
            <el-button type="primary">立即创建</el-button>
            <el-button @click="ResetForm">重置</el-button>
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
          return {
            UserForm: {
              username: '',
              password: '',
              permission: [],
              usertype: '',
            }
          }
        },
      methods: {
        ResetForm() {
          this.$router.push('/userList')
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
