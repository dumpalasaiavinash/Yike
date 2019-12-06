
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:yike_mobile_app/Pages/login_pge.dart';

import 'complaits.dart';

class Splash extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _SplashState();
  }
}

class _SplashState extends State<Splash> {

  
  nextscreen() async {
    
    if(await getValuesSF("logged", "bool")){
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => ComplaintPage()));
    }
    else Navigator.pushReplacement(context,MaterialPageRoute(builder: (context) =>LoginPage()));
  }

  var scaff = Scaffold(
      body: Container(
        color: Colors.indigo,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Text(
                  "YIKE",
                  style: TextStyle(fontSize: 72, color: Colors.white),
                ),
              ],
            )
          ],
        ),
      ),
    );


  @override
  initState() {
    super.initState();
    nextscreen();
  }

  @override
  Widget build(BuildContext context) {
    return scaff;
  }
}


getValuesSF(String key, String tYpe) async {
    if (tYpe.toLowerCase() == "string") {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      return prefs.getString(key);
    } else if (tYpe.toLowerCase() == "integer") {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      return prefs.getString(key);
    }
    else if (tYpe.toLowerCase() == "bool") {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      if(prefs.getBool(key)!=null)
       return prefs.getBool(key);
       return false;
    }
  }