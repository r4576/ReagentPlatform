// 필요한 모듈 선언
var createError = require("http-errors");
var express = require("express");
var path = require("path");
var cookieParser = require("cookie-parser");
var logger = require("morgan");
var fs = require("fs");

// 라우팅 모듈 선언
var indexRouter = require("./routes/index");
var usersRouter = require("./routes/users");
var contentsRouter = require("./routes/contents");

var app = express();

// port 선언
// app.listen(8000, function () {
//   console.log("Server Start!!");
// });

// express 서버 포트 설정
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));

//request 요청 URL과 처리 로직을 선언한 라우팅 모듈 매핑
app.use("/", indexRouter);
app.use("/users", usersRouter);
app.use("/contents", contentsRouter);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get("env") === "development" ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render("error");
});

module.exports = app;
