import 'package:flutter/material.dart';

class SignupButton extends StatelessWidget {
  final Widget icon;
  final Widget tittle;
  final Function onpressed;
  SignupButton({this.icon, this.tittle,this.onpressed});
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Container(
      height: 50,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: <Widget>[
          Expanded(child:Text(""),),
          Expanded(
            child: Container(
              padding: EdgeInsets.all(10),
              child: icon,
            ),
          ),
          Expanded(
            flex: 4,
            child: Container(
              child: InkWell(
                onTap: onpressed,
            child: 
              tittle,
            ),
            ),
          )
        ],
      ),
      decoration: BoxDecoration(
        gradient: LinearGradient(colors: <Color>[
                 Colors.indigoAccent,
                Colors.indigo
                
        ]),
        borderRadius: BorderRadius.circular(40.0),
        boxShadow: [
          BoxShadow(
            color: Colors.grey[500],
            offset: Offset(0.0, 1.5),
            blurRadius: 1.5,
          ),
        ],
      ),
      margin: EdgeInsets.all(16),
    );
  }
}
