<template>
  <div class="userlist">
    <top-header></top-header>
    <div id="table">
      <el-table
        :data="tableData"
        style="width: 100%">
        <el-table-column
          type="index"
          width="80">
        </el-table-column>
        <el-table-column
          label="用户名"
          width="180">
          <template slot-scope="scope">
            <i class="el-icon-user"></i>
            <span style="margin-left: 10px">{{ scope.row.username }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="角色"
          width="180">
          <template slot-scope="scope" >
            <el-popover trigger="hover" placement="top">
              <!--              权限: <p v-for="item in scope.row.permission"><span><el-tag effect="dark" >{{item}}</el-tag></span></p>-->
              <p>权限:<span v-for="item in scope.row.permission"><el-tag class="tag" effect="dark">{{item}}</el-tag></span></p>
              <div slot="reference" class="name-wrapper">
                <el-tag size="medium">{{ scope.row.role }}</el-tag>
              </div>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column
          label="状态"
          width="230" align="center">
          <template slot-scope="scope">
            <!--            <i class="el-icon-time"></i>-->
            <el-switch
              v-model="scope.row.status"
              on-color="#00A854"
              on-text="启动"
              on-value= "1"
              off-color="#F04134"
              off-text="禁止"
              off-value="0"
              @change="changeSwitch(scope.row)">
            </el-switch>
            <!--            <span style="margin-left: 10px">{{ scope.row.status }}</span>-->
          </template>
        </el-table-column>
        <el-table-column
          label="创建时间"
          width="220">
          <template slot-scope="scope">
            <i class="el-icon-time"></i>
            <span style="margin-left: 10px">{{ scope.row.createtime }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              size="mini"
              @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-dialog title="修改密码" :visible.sync="dialogFormVisible">
        <el-form>
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
        name: "userList",
        components: {TopHeader},
        data() {
          return {
            tableData: [
              // {
              //   "username" : "张三",
              //   "createtime": "2019-06-28 11:35:19",
              //   "status": "False",
              //   "role": "普通用户",
              //   "permission": ["查","增",'删']
              // }
            ],
            dialogFormVisible: false,
            UpwForm: {
                "username": '',
                "newpwd": ''
              }
          }
        },
      methods: {
        handleDelete(index,row) {
          this.$confirm('此操作将永久删除该用户, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            let username = row['username'];
            this.$http.post('/delete',{'username':username})
              .then(res => {
                let msg = res.data['message'];
                this.$message({
                  type: 'success',
                  message: msg
                });
                this.$router.go(0)
              }).catch(error => {
                let stat = error.response.status;
                let msg = error.response.data["message"];
                if (stat === 403) {
                  this.$message({
                    type: 'info',
                    message: msg
                  });
                } else {
                  this.$message({
                    type: 'info',
                    message: "请求失败"
                  });
                }
            });
            // this.tableData.splice(index,1);
          }).catch(error => {
            console.log(error)
            this.$message({
              type: 'info',
              message: '已取消删除'
            });
          });
        },
        changeSwitch (data) {
          let username = data['username'];
          let stat = data['status'];
          this.$http.post('/lock',{'username':username,'userlock':stat})
            .then(res => {
              if (stat === true) {
                this.$message({
                  message: '账号已锁定',
                  type: 'success'
                })
              }
              if (stat === false){
                this.$message({
                  message: '取消锁定',
                  type: 'success'
                })
              }
            }).catch( error => {
            this.$message({
              message: '执行失败',
              type: 'info'
            })
          });
          console.log(data)
        },
        handleEdit(index,row) {
          this.dialogFormVisible = true;
          let username = row['username'];
          this.UpwForm.username = username;
        },
        handleup() {
          this.dialogFormVisible = false;
          this.$http.post('/admin/upwd',{username:this.UpwForm.username,newpwd:this.UpwForm.newpwd})
            .then(res => {
              this.$message({
                message: '修改成功',
                type: 'success'
              });
            }).catch(error => {
              let stat = error.response.status;
              let msg = error.response.data['message'];
              if (stat === 403) {
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
        }
      },
      mounted() {
          this.$http.get('/userlist')
            .then(res => {
              let data = res.data['data'];
              this.tableData = data;
            }).catch(error => {
              let stat = error.response.status;
              if (stat === 403) {
                this.$message({
                  message: '无权限访问',
                  type: 'info'
                });
                this.$router.push('/home')
              } else {
                this.$message({
                  message: '请求失败',
                  type: 'info'
                });
              }
          })
      }
    }
</script>

<style scoped>
  .userlist{
    margin: 35px auto;
    width: 65%;
  }
  #table {
    margin: 35px auto;
    width: auto;
  }
  .tag {
    margin: 10px;
  }
</style>
