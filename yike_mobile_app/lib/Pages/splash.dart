import 'dart:async';

import 'package:flutter/material.dart';


class Splash extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    // TODO: implement createState
    return _SplashState();
  }
}

class _SplashState extends State<Splash> {
  Timer _timer;
  @override
  void initState() {
    super.initState();
    /* _timer = new Timer(const Duration(milliseconds: 400), () {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => LoginPage()),
      );
    });
*/
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Color.fromRGBO(70, 70, 255, 1),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Text(
                "yIKE",
                style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 48,
                    color: Colors.white),
              )
            ],
          )
        ],
      ),
    );
  }
}
