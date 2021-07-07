var express = require("express");

var path = require("path");

var createError = require("http-errors");
var cookieParser = require("cookie-parser");
var logger = require("morgan");
var dateFormat = require("dateformat");

var indexRouter = require("./routes/index");
var usersRouter = require("./routes/users");
var tablesRouter = require("./routes/tables");
var chartsRouter = require("./routes/charts");
// var reagentRouter = require("./routes/reagent");
// var nmrRouter = require("./routes/nmr");
// var catalystRouter = require("./routes/catalyst");

var app = express();

// view engine setup
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));

app.use("/", indexRouter);
app.use("/users", usersRouter);
app.use("/tables", tablesRouter);
app.use("/charts", chartsRouter);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  console.log("[" + dateFormat(new Date(), "dd/mmm/yyyy HH:MM:ss") + "] " + err.message);
  res.locals.message = err.message;
  res.locals.error = req.app.get("env") === "development" ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render("error");
});

module.exports = app;
