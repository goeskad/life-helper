以下场景，我们需要在 JS 中处理数据并进行文件下载。

纯前端处理文件流：在线格式转换、解压缩等
整个数据都在前端转换处理，压根没有服务端的事
文章所要讨论的情况
接口鉴权：鉴权方案导致请求必须由 JS 发起，如 cookie + csrfToken、JWT
使用 ajax ：简单但是数据都在内存中
（推荐）使用 iframe + form 实现：麻烦但是可以由下载线程流式下载
服务端返回文件数据，前端转换处理后下载
如服务端返回多个文件，前端打包下载
（推荐）去找后端 ~~聊一聊~~