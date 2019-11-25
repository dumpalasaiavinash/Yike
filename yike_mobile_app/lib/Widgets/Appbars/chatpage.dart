import 'package:flutter/material.dart';

class ChatPageAppBar extends StatelessWidget{
  @override
  PreferredSizeWidget build(BuildContext context) {
    // TODO: implement build
    return AppBar(
      leading: CircleAvatar(backgroundColor: Colors.white,),
      title:Column(children: <Widget>[
          Text("Company Pvt. Ltd.", style: TextStyle(color: Colors.white,fontSize: 16),),
          Text("Agent_name",style:TextStyle(fontSize: 12,color: Colors.white))
        ],) ,
         /* Container(decoration: BoxDecoration(color: Colors.blue),
    child:Row(
      children: <Widget>[
        Expanded(child: CircleAvatar(backgroundColor: Colors.white,),flex: 2,),
        Expanded(child: Column(children: <Widget>[
          Text("Company Pvt. Ltd.", style: TextStyle(color: Colors.white,fontSize: 16),),
          Text("Agent_name",style:TextStyle(fontSize: 12,color: Colors.white))
        ],),flex: 8,)
        
      ],
      
    )
    );*/
    );
  }
}