<template>
    <div class="about">
      <top-header></top-header>
      <div class="card">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>关于</span>
            <el-button style="float: right; padding: 3px 0" type="text" @click="upavatar">更新头像</el-button>
          </div>
          <div class="avatar" >
            <el-avatar shape="square" :size="100" :src="UserInfo.avatar"></el-avatar>
          </div>
          <div class="text item">
            <span @click="dialogFormVisible = true">{{UserInfo.username}}</span>
          </div>
          <div class="permission">
            <el-popover trigger="hover" placement="bottom">
              <span v-for="item in UserInfo.permission"><el-tag class="tag" effect="dark">{{item}}</el-tag></span>
              <div slot="reference" class="name-wrapper">
                <el-tag size="medium" effect="dark">{{ UserInfo.role }}</el-tag>
              </div>
            </el-popover>
          </div>
          <div class="info">
            <p @click="setabout">{{UserInfo.description}}</p>
          </div>
        </el-card>
        <el-dialog title="修改密码" :visible.sync="dialogFormVisible">
          <el-form>
            <el-form-item label="旧密码">
              <el-input v-model="UpwForm.oldpwd" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="新密码">
              <el-input v-model="UpwForm.newpwd"  autocomplete="off"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="handleup">确 定</el-button>
          </div>
        </el-dialog>
      </div>
    </div>
</template>

<script>
    import TopHeader from "../../common/top-header";
    export default {
        name: "about",
        components: {TopHeader},
        data() {
          return {
            // url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
            UserInfo: {
              "username": "",
              "role": "",
              "avatar": '',
              "permission": [],
              "description": "我不是英雄，我只做我想做的事，保护我想要保护的人而已。"
            },
            dialogFormVisible: false,
            UpwForm: {
              'oldpwd': '',
              'newpwd': ''
            }
          }
        },
      methods: {
        setabout() {
          this.$prompt('请输入简介','提示',{
            confirmButtonText: '确定',
            cancelButtonText: '取消',
          })
            .then(({value}) => {
              this.$http.post('/description',{username:this.UserInfo.username,description:value})
                .then(res =>{
                  this.$message({
                    type: 'success',
                    message: '已经修改'
                  });
                  this.UserInfo.description = value;
                }).catch(error => {
                this.$message({
                  type: 'info',
                  message: '修改失败'
                });
              });
            })
            .catch(() => {
              this.$message({
                type: 'info',
                message: '取消输入'
              });
            })
        },
        handleup() {
          this.dialogFormVisible = false;
          let oldpwd = this.UpwForm.oldpwd;
          let newpwd = this.UpwForm.newpwd;
          this.$http.post('/upwd',{username:this.UserInfo.username,oldpwd:oldpwd,newpwd:newpwd})
            .then(res => {
              this.$message({
                message: '修改成功',
                type: 'success'
              });
              localStorage.removeItem('Authorization');
              this.$router.push('/')
            }).catch(error => {
              let stat = error.response.status;
              let msg = error.response.data['message'];
              if (stat === 403 || stat === 401) {
                this.$message({
                  message: msg,
                  type: 'info'
                });
              } else {
                this.$message({
                  message: '修改失败',
                  type: 'info'
                });
              }
          })
        },
        upavatar() {
          this.$http.get('/upavatar')
            .then(res=> {
              let src = res.data["message"];
              this.UserInfo.avatar = src
            })
        }
      },mounted() {
        this.$http.get('/about')
          .then(res => {
            let user = res.data['data'];
            this.UserInfo = user;
          })
      }
    }
</script>

<style scoped>
.about{
  margin: 35px auto;
  width: 65%;
}
.clearfix{
  text-align: left;
}
.card{
  text-align: center;
  margin: 35px auto;
  width: 70%;
}
.text {
  margin-top: 2em;
  font-size: larger;
}
.tag {
  margin: 10px;
}
.permission {
  margin-top: 1em;
  margin-bottom: 2em;
}
.info {
  font-size: larger;
}
</style>
