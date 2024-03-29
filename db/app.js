var express = require('express');

var createError = require('http-errors');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var dateFormat = require("dateformat");

var createRouter = require('./routes/create');

var app = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

app.use('/create', createRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  console.log("[" + dateFormat(new Date(), "dd/mmm/yyyy HH:MM:ss") + "] " + err.message);
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
});

module.exports = app;
