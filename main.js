var express      = require('express')
var cookieParser = require('cookie-parser')

var sqlite3 = require("sqlite3").verbose();
var db= new sqlite3.Database("/home/vedant/flask/Signin_up/login_check.db");

var app = express()
app.use(cookieParser())

app.get('/', function(req, res) {
  var status=0;
  session = req.cookies.session;

  db.serialize(function(){
  if(!session)
  {
	res.send("You are not logged in");
  }
  else	
  {
	db.all("SELECT * from login_status where session_id='"+session+"'",function(err,row){
	if(row.length>0)
	{
		if(row[0].status=="logged_in")
		{
			res.send("You are logged in");	
		}
		else
		{
			res.send("You are logged out");
			return;
		}
	}
	else
	{
		console.log("Hello");
		res.send("Pliss to not play with the session id ");
		return;	
	}
});
  }
});

});


app.listen(8081);

