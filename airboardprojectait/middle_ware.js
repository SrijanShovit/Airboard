function sessionMiddleware(){
    app.use(express.urlencoded({extended:true}))
    app.use(
        session({
        secret: 'keyboard cat',
        resave: false,
        saveUninitialized: false,
        store: new MongoStore({ mongooseConnection: mongoose.connection }),
        })
    )
    // Passport middleware
    app.use(passport.initialize())
    app.use(passport.session())
}
const session_Middleware= sessionMiddleware()
module.exports= session_Middleware;
