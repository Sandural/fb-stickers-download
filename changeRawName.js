/**
 * @Description  :
 * @Author       : Lizishan
 * @Date         : 2020-09-19 12:49:32
 * @LastEditors  : Lizishan
 * @LastEditTime : 2020-09-19 20:30:06
 * @FilePath     : /sticker2gif/changeRawName.js
 */
var fg = require("fast-glob");
var pixels = require("image-pixels");
var fs = require('fs')

const MAX_ROWS = 7;
const MAX_COLUMNS = 7;
let finallResultRows = null;
let finallResultColumns = null;

function isXSepLine(y, width, imgData) {
  let initValue = "";
  // 此处有公式
  let startPos = width * y * 4;
  let endPos = width * (y + 1) * 4;
  for (let i = startPos; i < endPos; i += 4) {
    let tv = `${imgData[i]}.${imgData[i + 1]}.${imgData[i + 2]}.${
      imgData[i + 3]
    }`;
    if (initValue) {
      if (initValue !== tv) {
        return false;
      }
    } else {
      initValue = tv;
    }
  }
  return true;
}

function isYSepLine(x, height, width, imgData) {
  let initValue = "";
  // 此处有公式
  let startPos = x * 4;
  let endPos = width * (height - 1) * 4;
  for (let i = startPos; i < endPos; i += width * 4) {
    let tv = `${imgData[i]}.${imgData[i + 1]}.${imgData[i + 2]}.${
      imgData[i + 3]
    }`;
    if (initValue) {
      if (initValue !== tv) {
        return false;
      }
    } else {
      initValue = tv;
    }
  }
  return true;
}

/**
 * 
 * @param {*} index: 行几等分
 * @param {*} height
 * @param {*} width 
 * @param {*} colorArrData
 */
function isCanRow(index, height, width, colorArrData) {
  // dis 每等分的宽度
  let dis = Math.floor(height / index);
  // console.log('row', dis, height, index)
  for (let i = dis; i < height; i += dis) {
    // i：行分割线的高度长，index-1 条线
    // 判断这条线是不是分割线
    if (!isXSepLine(i, width, colorArrData)) {
      // index - 1条线中， 只要有1条不是分割线， 那就意味着切到图了， 然后退出， 进行下一等分切割
      return false;
    }
  }
  // 可以等分，记录每等分的长度（dis）的最小值：即等分的最大值
  // if(finallResultRows === null || dis < finallResultRows) 
  finallResultRows = dis;
  return true;
}

function isCanCol(index, height, width, colorArrData) {
  let dis = Math.floor(width / index);
  // console.log('col', dis, width, index)
  // 认定是能分割的
  for (let i = dis; i < width; i += dis) {
    // console.log('col', i)
    if (!isYSepLine(i, height, width, colorArrData)) {
      // console.log(`col 这里不能${index%2==0 ? '偶' : '奇'}分`, i, index)
      return false;
      // }
    }
  }
  // if(finallResultColumns === null || dis < finallResultColumns) 
  finallResultColumns = dis;
  return true;
}

// 修改文件名称
function rename (oldPath, newPath) {
  fs.rename(oldPath, newPath, function(err) {
      if (err) {
          throw err;
      }
  });
}

let rawPath = 'images/Cute/raw'
let fileArr = fg.sync("images/Cute/raw/*.png");
(async () => {
  for (let i = 0; i < fileArr.length; i++) {
    // 单张图片高宽上限为10000
    finallResultRows = null;
    finallResultColumns = null;

    // 尝试值：尝试把整张图几等分，默认1x1, 即原图
    let MaxRow = 1;
    let MaxCol = 1;

    // data: 图片像素 unit8Array; width/height: 图片的高宽
    let { data, width, height } = await pixels(fileArr[i]);

    // 把 unit8Array 转成 string
    let colorArrData = data.toString().split(",");

    // 需要区分奇偶等分，不可分割是 不可奇分 也不可 偶分
    // 设定行等分最大值 7， 一直从2等分计算到7等分
    while (MaxRow < MAX_ROWS) {
      isCanRow(++MaxRow, height, width, colorArrData);
    }
    // 设定列等分最大值 7， 一直从2等分计算到7等分
    while (MaxCol < MAX_COLUMNS) {
      isCanCol(++MaxCol, height, width, colorArrData);
    }
    console.log(`rows: ${height / finallResultRows}  columns: ${width / finallResultColumns} file: ${fileArr[i]}`);
    let newPath = `${rawPath}/${fileArr[i].split('/')[3].split('_')[0]}-${width}x${height}-${height / finallResultRows}x${width / finallResultColumns}.png`
    rename(fileArr[i], newPath)

  }
})();
