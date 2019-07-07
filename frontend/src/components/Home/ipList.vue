<template>
  <div class="iplist">
    <top-header></top-header>
    <div id="table">
      <el-table :data="proxypools" style="width: 100%">
        <el-table-column
          type="index"
          width="50">
        </el-table-column>
        <el-table-column label="Ip" width="160">
          <template slot-scope="scope">
            <el-popover trigger="hover" placement="top">
              <p>地址: {{ scope.row.address }}</p>
              <p>运营商: {{ scope.row.isp }}</p>
              <div slot="reference" class="name-wrapper">
                <el-tag size="medium">{{ scope.row.ip }} : {{ scope.row.port }}</el-tag>
              </div>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column label="类型" width="90">
          <template slot-scope="scope">
            <i class="el-icon-info"></i>
            <span style="margin-left: 10px">{{ scope.row.httptype }}</span>
          </template>
        </el-table-column>
        <el-table-column label="响应时间"  width="160">
          <template slot-scope="scope">
            <i class="el-icon-loading"></i>
            <span style="margin-left: 10px">{{ scope.row.spend }}毫秒</span>
          </template>
        </el-table-column>
        <el-table-column label="验证时间" >
          <template slot-scope="scope">
            <i class="el-icon-time"></i>
            <span style="margin-left: 10px">{{ scope.row.createtime }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              size="mini"
              :plain="true"
              @click="handleEdit(scope.$index, scope.row)" >复制</el-button>
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>

</template>

<script>
    import TopHeader from "../../common/top-header";
    export default {
        name: "ipList",
        components: {TopHeader},
        data() {
          return {
            proxypools: [
              // {
              //   ip: '112.85.130.136',
              //   port: 9999,
              //   httptype: 'HTTP',
              //   address: '',
              //   operator: '',
              //   spend: '2.3',
              //   createtime: '2019-06-18 16:16:11',
              // },
            ]
          }
        },
      methods: {
        handleEdit(index, row) {
          var ip = row['ip'];
          var port = row['port'];
          var ipport = ip + ":" + port;
          let _this = this;
          _this.$copyText(ipport).then(function (e) {
            _this.$message({
              message: '内容已复制',
              type: 'success'
            });
          },function (e) {
            _this.$message(e);
          })
        },
        handleDelete(index, row) {
          this.proxypools.splice(index,1);
        }
      },
      mounted() {
          console.log(localStorage.getItem("Authorization"));
          this.$http.get('/iplist')
            .then(res => {
              let data = res.data;
              console.log(data);
              this.proxypools = data["data"]
            }).catch(error => {
              this.$message({
                message: '请求失败',
                type: 'info'
              })
          })
      }
    }
</script>

<style scoped>
  .iplist{
    margin: 35px auto;
    width: 65%;
  }
  #table {
    margin: 35px auto;
    width: auto;
  }
</style>
