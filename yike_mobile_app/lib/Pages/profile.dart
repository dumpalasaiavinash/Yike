import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:yike_mobile_app/Widgets/Buttons/raised_gradient_button.dart';

import 'login_pge.dart';

logout() async{
    SharedPreferences prefs = await SharedPreferences.getInstance();
      prefs.setBool("logged", false);
}

class ProfilPage extends StatelessWidget{
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
      Container(child:Text("Yashwanth Kikkuri",style: TextStyle(fontSize: 18,),),margin: EdgeInsets.only(top:100,left:16), ),
      Container(child: Text("yashukikkuri@gmail.com", style: TextStyle(color: Colors.indigoAccent),), margin: EdgeInsets.only(top: 8,left:16,right: 16),),
      Container(child:RaisedGradientButton(child: Text("Log Out"),gradient: LinearGradient(colors: [
        Colors.indigoAccent,
        Colors.indigoAccent,
      ]),
      onPressed:(){
        logout();
        Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => LoginPage()));}
      ),
      margin: EdgeInsets.only(top:24,
      left: MediaQuery.of(context).size.width*0.1,
      right: MediaQuery.of(context).size.width*0.1),)
      
      
    ],);
  }
  
}