const express=require("express")
require('dotenv').config();

// const mongoose=require('mongoose')
// const passport = require('passport')
// const session = require('express-session')
// const MongoStore = require('connect-mongo')
// require('dotenv').config({ path: './config/config.env' })
// require("./config/passport")(passport)

const app=express()
app.set('view engine','ejs');
// const PORT = process.env.PORT||3000;


// mongoose.connect(process.env.MONGO_URI,{
//     useNewUrlParser:true,
//     useUnifiedTopology: true
// })
app.use(express.static(__dirname + '/public'));
// app.use(express.static('public'))

//*-------------------------session middleware--------------------------------
// app.use(express.urlencoded({extended:true}))
// app.use(
//     session({
//       secret: 'keyboard cat',
//       resave: false,
//       saveUninitialized: false,
//       store: MongoStore.create({ mongoUrl: process.env.MONGO_URI }),
//     })
//   )
//   // Passport middleware
// app.use(passport.initialize())
// app.use(passport.session())

//*---------------------------------------------------------

//*-----------Importing  routes-------------
// app.use(require("./routes/index"))
// app.use('/auth', require('./routes/auth'))
//*-----------------------------------------


// app.listen(PORT,console.log(`listening at ${PORT}`))

app.get("/", (req, res) => {
//   var api_url = process.env.API_URL
//   const response = await fetch(api_url,{
//     method:'get',
//     headers:{"Authorization":`Token ${document.cookie.valueOf('authtoken').split("authtoken=")[1].split(";")[0]}`}
// })
//   console.log(response);
    // .then(res => res.json())
    // .then(data => {
    //   res.render("teams",{teams:data});
    // })
  res.render("teams",{apiurl:process.env.API_URL})
  // res.render("track")
  // res.render("home")s
})
app.get("/teams/:team_id",(req,res) =>{
  res.render("team_page");

})
app.get("/signup",(req, res) => {
  res.render("signup",{apiurl:process.env.API_URL})
})

app.get("/login",(req, res) => {
  res.render("login",{apiurl:process.env.API_URL})
})

app.listen(3300)