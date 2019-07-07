<template>
  <div>
    <top-header></top-header>
    <div class="Progress">
      <el-progress :percentage="50"></el-progress>
      <el-progress :percentage="100" :format="format"></el-progress>
      <el-progress :percentage="100" status="success"></el-progress>
      <el-progress :percentage="100" status="warning"></el-progress>
      <el-progress :percentage="50" status="exception"></el-progress>

      <el-progress :text-inside="true" :stroke-width="26" :percentage="70"></el-progress>
      <el-progress :text-inside="true" :stroke-width="24" :percentage="100" status="success"></el-progress>
      <el-progress :text-inside="true" :stroke-width="22" :percentage="80" status="warning"></el-progress>
      <el-progress :text-inside="true" :stroke-width="20" :percentage="50" status="exception"></el-progress>
    </div>
  </div>
</template>

<script>

    import TopHeader from "../../common/top-header";
    export default {
        name: "chart",
      components: {TopHeader},
      methods: {
        format(percentage) {
          return percentage === 100 ? '满' : `${percentage}%`;
        }
      }
    }
</script>

<style>
.Progress{
  margin-top: 4em;
  padding: 90px;
}
</style>
