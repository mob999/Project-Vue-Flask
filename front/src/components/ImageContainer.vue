<template>
    <div id="root">
        <el-dialog title="图像预览" :visible.sync="tpDialogVisible" width="1000px" height="400px" style="z-index:0;">
              <el-image
              :src="drawUrl"
              style="width: 70%; height: 70%"
              fit="scale-down"
              ></el-image>
        </el-dialog>
        <el-dialog title="图像预览" :visible.sync="oriDialogVisible" width="1000px" height="400px" style="z-index:0;">
              <el-image
              :src="originUrl"
              style="width: 70%; height: 70%"
              fit="scale-down"
              ></el-image>
        </el-dialog>
        <div id="word">
          <h1>{{ msg }}</h1>
          服务端状态：{{serveStatus}}
        </div>
        <div class="content">
          <div class="controller">
            <el-select
              v-model="yoloModel"
              placeholder="请选择yolo模型"
              @visible-change="getModels"
              @change="changeModels('yolo')"
              class="controlles"
              >
              <el-option
                v-for="item in yoloWeights"
                :key="item"
                :lable="item"
                :value="item"
              >
              </el-option>
            </el-select>
            <el-select
            v-model="lprModel"
            placeholder="请选择lprnet模型"
            @visible-change="getModels"
            @change="changeModels('lprnet')"
            class="controlles"
            >
              <el-option
                v-for="item in lprWeights"
                :key="item"
                :lable="item"
                :value="item"
              >
              </el-option>
            </el-select>
            <el-button
             @click="getDefaultModel"
             style = "padding-right:10px"
            >
              载入上次（默认）模型
            </el-button>
            <el-button
            @click="upload"
            class="controlles"
            >
              上传图片<i class="el-icon-upload el-icon--right">{{filename}}</i>
            </el-button>
          </div>
          <input
            ref="upload"
            style="display:none"
            name="file"
            type="file"
            @change="updateImage"
          />
          <el-dialog
            title="提示"
            :visible.sync="dialogVisible"
            width="30%">
            <span>图片上传中</span>
            <span slot="footer" class="dialog-footer">
              <el-button @click="dialogVisible = false">隐藏</el-button>
            </span>
          </el-dialog>
          <el-dialog
            title="提示"
            :visible.sync="errorDialog"
            width="30%">
            <span>{{errMsg}}</span>
            <span slot="footer" class="dialog-footer">
              <el-button @click="errorDialog = false">关闭</el-button>
            </span>
          </el-dialog>
          <div class="imgtype">
            <div style="margin:auto">原图</div>
            <div style="margin:auto">检测结果</div>
          </div>
              <div class="two-image-box">
                  <el-image
                    class="image-box"
                    :src="originUrl"
                    fit="scale-down"
                    @click="openImage('origin')"
                  >
                    <div slot="error" class="image-slot" style="margin-top:100px">
                      <el-empty description="暂无数据"></el-empty>
                    </div>
                  </el-image>

                  <el-image
                    class="image-box"
                    :src="drawUrl"
                    fit="scale-down"
                    @click="openImage('draw')"
                  >
                    <div slot="error" class="image-slot" style="margin-top:100px">
                      <el-empty description="暂无数据"></el-empty>
                    </div>
                  </el-image>
              </div>

            <el-table :data="tableData" style="width:90%;margin-left:5%;margin-right:5%;margin-top:20px;" @cell-click="cell_click">
              <el-table-column prop="name" label="图片名称" >
              </el-table-column>
              <el-table-column prop="size" label="图片大小">
              </el-table-column>
              <el-table-column prop="res" label="识别结果">
              </el-table-column>
              <el-table-column prop="conf" label="置信度">
              </el-table-column>
            </el-table>
          </div>
    </div>
</template>

<script>
import axios from 'axios'
import Viewer from 'viewerjs'
export default {
  name: 'ImageContainer',
  comments: {
    'viewer': Viewer
  },
  data () {
    return {
      originUrl: '',
      drawUrl: '',
      msg: '基于YOLOV5和LPRnet的车牌检测',
      dialogVisible: false,
      filename: '',
      errorDialog: false,
      result: '',
      imgSize: '',
      tableData: [],
      errMsg: '',
      yoloWeights: [],
      lprWeights: [],
      yoloModel: '',
      lprModel: '',
      hasGotModels: false,
      tpDialogVisible: false,
      oriDialogVisible: false,
      serveStatus: '未连接'
    }
  },
  mounted () {
    axios.get(this.serveUrl('test')).then(() => {
      this.serveStatus = '已连接'
      console.log(this.serveStatus)
    }).catch(() => {
      this.serveStatus = '未连接'
      console.log(this.serveStatus)
    })
  },

  methods: {
    upload () {
      console.log('haha')
      this.$refs.upload.click()
    },
    serveUrl (s) {
      return 'http://region-4.autodl.com:47238/' + s
    },
    openImage (type) {
      console.log(type)
      if (type === 'draw') {
        this.tpDialogVisible = true
      } else if (type === 'origin') {
        this.oriDialogVisible = true
      }
    },
    cell_click (row) {
      this.originUrl = this.originUrl.substring(0, this.originUrl.lastIndexOf('/') + 1) + row.name
      this.drawUrl = this.drawUrl.substring(0, this.drawUrl.lastIndexOf('/') + 1) + row.name
    },
    updateImage (e) {
      console.log('updateImage')
      let _img = e.target.files[0]
      let imgType = _img.name.substring(_img.name.lastIndexOf('.') + 1)
      if (imgType !== 'jpg') {
        this.errorDialog = true
        this.errMsg = '图片格式必须为jpg'
        return
      }
      let timer = setInterval(() => {
      }, 50)
      let config = {
        header: {'Content-Type': 'multipart/form-data'}
      }
      let param = new FormData()
      param.append('file', _img, _img.name)
      this.filename = _img.name
      this.dialogVisible = true
      axios
        .post(this.serveUrl('upload'), param, config)
        .then((response) => {
          clearInterval(timer)
          this.originUrl = response.data.origin_url
          console.log(this.originUrl)
          this.drawUrl = response.data.draw_url
          this.result = response.data.result.split(' ')[0]
          this.imgSize = response.data.img_size.split(' ')[0]
          this.confidence = response.data.result.split(' ')[1]
          this.dialogVisible = false
          this.tableData.push({
            'name': this.filename,
            'size': this.imgSize,
            'res': this.result,
            'conf': this.confidence
          })
          if (this.result === '') {
            this.$notify.error({
              title: '失败',
              message: '检测失败，未识别到车牌'
            })
          } else {
            this.$notify({
              title: '成功',
              message: '图片上传及检测成功!',
              type: 'success'
            })
            this.$message({
              message: '点击图片可查看预览,点击检测记录表格可查看历史检测图',
              type: 'success'
            })
          }
        })
        .catch(() => {
          this.dialogVisible = false
          this.$message.error({
            message: '图片上传失败，服务端未连接'
          })
        })
      console.log(this.drawUrl)
    },
    getModels () {
      if (this.hasGotModels === true) {
        return
      }
      this.yoloWeights = []
      this.lprWeights = []
      axios
        .get(this.serveUrl('get-models'))
        .then((response) => {
          let allWeights = response.data.split(' ')
          for (let i = 0; i < allWeights.length; i++) {
            let type = allWeights[i].substring(allWeights[i].lastIndexOf('.') + 1)
            if (type === 'pt') {
              this.yoloWeights.push(allWeights[i])
            } else if (type === 'pth') {
              this.lprWeights.push(allWeights[i])
            }
          }
          this.hasGotModels = true
        })
        .catch(() => {
          this.dialogVisible = false
          this.$message.error({
            message: '模型列表载入失败，服务端未连接'
          })
        })
    },
    changeModels (type) {
      let param = {'type': type, 'name': type === 'yolo' ? this.yoloModel : this.lprModel}
      axios
        .get(this.serveUrl('change-models'), {
          params: param
        })
        .then((response) => {
          this.$notify({
            title: '成功',
            message: '模型更换成功',
            type: 'success'
          })
        })
        .catch(() => {
          this.dialogVisible = false
          this.$message.error({
            message: '模型更换失败，服务端未连接'
          })
        })
    },
    getDefaultModel () {
      axios
        .get(this.serveUrl('get-cur-model'))
        .then((response) => {
          this.yoloModel = response.data.det_weights.split('/')[2]
          this.lprModel = response.data.rec_weights.split('/')[2]
          this.$notify({
            title: '成功',
            message: '模型载入成功',
            type: 'success'
          })
        })
        .catch(() => {
          this.dialogVisible = false
          this.$message.error({
            message: '模型载入失败，服务端未连接'
          })
        })
    }
  }
}
</script>

<style>
  #root {
    height: 100%;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    background-color: rgb(51, 51, 51)
  }
  #word {
    padding-top: 20px;
    padding-bottom: 20px;
    border-bottom-color: darkgray;
    border-bottom-style: solid;
    border-bottom-width: 1px;
  }
  .content {
    height: 100%;
    background-color: white;
    color:black;
  }

  .two-image-box {
    width: 90%;
    height: 500px;
    display: flex;
    margin-bottom: 10px;
    margin-left: 5%;
    margin-right: 5%;
  }

  .image-box {
    width: 50%;
    margin:5px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    height: 100%;
    background-color:white;
  }

  .controller {
    display: flex;
    width: 90%;
    margin-left: 5%;
    margin-right: 5%;
    margin-bottom: 20px;
    padding-top: 10px;
  }

  .imgtype {
    display: flex;
    width:90%;
    margin-left: 5%;
    margin-right: 5%;
  }

  .controlles {
    padding-right: 20px;
  }

</style>
