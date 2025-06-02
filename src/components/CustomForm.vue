<template>
  <!-- 商家信息表单，包含多种输入类型和详细注释 -->
  <form @submit.prevent="handleSubmit">
    <!-- 商家名称输入框 -->
    <div>
      <label for="merchantName">商家名称</label>
      <input id="merchantName" v-model="form.merchantName" type="text" required />
    </div>
    <!-- 商户ID输入框 -->
    <div>
      <label for="merchantId">商户ID</label>
      <input id="merchantId" v-model="form.merchantId" type="text" required />
    </div>
    <!-- 门店ID输入框 -->
    <div>
      <label for="storeId">门店ID</label>
      <input id="storeId" v-model="form.storeId" type="text" required />
    </div>
    <!-- 收银员输入框 -->
    <div>
      <label for="cashier">收银员</label>
      <input id="cashier" v-model="form.cashier" type="text" required />
    </div>
    <!-- 收款类型下拉选择 -->
    <div>
      <label for="paymentType">收款类型</label>
      <select id="paymentType" v-model="form.paymentType" required>
        <option value="">请选择</option>
        <option value="wechat">微信</option>
        <option value="alipay">支付宝</option>
        <option value="cash">现金</option>
        <option value="other">其他</option>
      </select>
    </div>
    <!-- 新增：就餐方式多选框 -->
    <div>
      <label>就餐方式</label>
      <div class="checkbox-group">
        <label>
          <input type="checkbox" value="堂食" v-model="form.diningOptions" /> 堂食
        </label>
        <label>
          <input type="checkbox" value="外卖" v-model="form.diningOptions" /> 外卖
        </label>
        <label>
          <input type="checkbox" value="打包" v-model="form.diningOptions" /> 打包
        </label>
      </div>
    </div>
    <!-- 提交按钮 -->
    <button type="submit">提交</button>
  </form>
</template>

<script setup>
import { reactive } from 'vue'

// 表单数据，包含所有字段
const form = reactive({
  merchantName: '', // 商家名称
  merchantId: '',   // 商户ID
  storeId: '',      // 门店ID
  cashier: '',      // 收银员
  paymentType: '',  // 收款类型
  diningOptions: [] // 就餐方式（多选）
})

// 表单提交处理函数
function handleSubmit() {
  // 这里可以根据需要处理表单数据，比如表单校验、API提交等
  console.log('提交数据', { ...form })
}
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 400px;
}
label {
  margin-bottom: 4px;
}
input, select {
  padding: 6px 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.checkbox-group {
  display: flex;
  gap: 16px;
  margin-top: 4px;
}
button {
  padding: 8px 16px;
  background: #409eff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background: #66b1ff;
}
</style> 