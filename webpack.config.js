var path = require('path');
var HtmlWebPackPlugin = require("html-webpack-plugin");
module.exports = {
    //development production none
    mode:"production",
    //项目入口
    entry: "./src/index.ts",
    //输出设置
    output: {
        filename: "bundle.js",
        path: path.resolve(__dirname, 'dist')
    },
    //调试工具
    devtool: "source-map",
    //模块加载器设置
    module: {
        rules:[
            {
                test:/\.(png|jpg)$/,
                //[ext]为后缀名占位符 [name]名字占位符 [hash:8]哈希占位符，可指定位数
                loader:'url-loader?limit=4096&name=src/[name].[ext]'
            },
            {
                //ts-loader 解决对类型定义文件 .d.ts的解析
                //在此项目中使用了类型定义文件，
                //但是由于tsconfig的include设置并没有让根目录的类型定义文件加载故先去除
                test:/\.tsx?$/,
                use:'ts-loader',
                exclude: /node_modules/
            }
        ]
    },
    //调试服务
    devServer: {
        contentBase: path.join(__dirname, "dist"),
        compress: true,
        port: 7777,
        host:'localhost'
    },
    //插件
    plugins: [
        new HtmlWebPackPlugin(
            {
                template:"./index.html",
                title: "threejs学习"
            }),
    ]
}