const express=require("express")
const mongoose=require('mongoose');
const dotenv = require('dotenv')
const passport = require('passport')
const session = require('express-session')
const MongoStore = require('connect-mongo')
require('./config/passport')(passport)


const app=express()
app.set('view engine','ejs');
// const PORT = process.env.PORT||3000;
dotenv.config({ path: './config/config.env' })

mongoose.connect(process.env.MONGO_URI,{
    useNewUrlParser:true,
    useUnifiedTopology: true
})
app.use(express.static(__dirname + '/public'));
// app.use(express.static('public'))

//*-------------------------session middleware--------------------------------
app.use(express.urlencoded({extended:true}))
app.use(
    session({
      secret: 'keyboard cat',
      resave: false,
      saveUninitialized: false,
      store: MongoStore.create({ mongoUrl: process.env.MONGO_URI }),
    })
  )
  // Passport middleware
app.use(passport.initialize())
app.use(passport.session())

//*---------------------------------------------------------

//*-----------Importing  routes-------------
app.use(require("./routes/index"))
app.use('/auth', require('./routes/auth'))
//*-----------------------------------------


// app.listen(PORT,console.log(`listening at ${PORT}`))

app.get("/", (req, res) => {
  // res.render("paint",{title:"Airboard"})
  // res.render("track")
  res.render("login");
})

// app.listen(3000)