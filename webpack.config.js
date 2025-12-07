const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

const entries = require("./frontend/static/entries.js");

// 👇 add this
const isProd = process.env.NODE_ENV === "production";

module.exports = {
  context: __dirname,

  entry: entries,

  output: {
    // 👇 point to frontend/static/bundles
    path: path.resolve(__dirname, "frontend/static/bundles/"),
    filename: "[name].bundle.js",
    publicPath: "/static/bundles/",
  },

  resolve: { extensions: [".js", ".jsx"] },

  module: {
  rules: [
    {
      test: /\.(js|jsx)$/,
      exclude: /node_modules/,
      use: "babel-loader",
    },
    {
      test: /\.css$/i,
      use: ["style-loader", "css-loader"],
    },
  ],
},


  optimization: {
    splitChunks: {
      chunks: "all",
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/](react|react-dom)/,
          name: "vendor",
          chunks: "all",
        },
        commons: {
          test: path.resolve(__dirname, "frontend/shared"),
          name: "commons",
          minChunks: 2,
        },
      },
    },
    runtimeChunk: "single",
  },

  plugins: [
    new CleanWebpackPlugin(),
    new BundleTracker({
      path: __dirname,
      filename: "webpack-stats.json",
    }),
  ],
  
   externals: {
    moment: "moment",
    wed: "wed",
  },

  mode: isProd ? "production" : "development",

  devtool: isProd ? "source-map" : "eval-cheap-module-source-map",
};
