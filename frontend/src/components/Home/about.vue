<template>
    <div class="about">
      <top-header></top-header>
      <div class="card">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>关于</span>
          </div>
          <div class="avatar" >
            <el-avatar shape="square" :size="100" :src="url"></el-avatar>
          </div>
          <div class="text item">
            <span>{{UserInfo.username}}</span>
            <el-tag effect="dark">
              {{ UserInfo.role }}
            </el-tag>
            <p @click="setabout">{{UserInfo.description}}</p>
          </div>
        </el-card>
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
            url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
            UserInfo: {
              "username": "张三",
              "role": "管理员",
              "description": "我不是英雄，我只做我想做的事，保护我想要保护的人而已。"
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
              this.$message({
                type: 'success',
                message: '已经添加'
              });
              this.UserInfo.description = value;
            })
            .catch(() => {
              this.$message({
                type: 'info',
                message: '取消输入'
              });
            })
        }
      }
    }
</script>

<style scoped>
.about{
  margin: 35px auto;
  width: 65%;
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
</style>
