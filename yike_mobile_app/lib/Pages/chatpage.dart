import 'package:flutter/material.dart';
import 'package:yike_mobile_app/Widgets/Footers/chatpage_footer.dart';
import 'package:yike_mobile_app/Widgets/recived_msg.dart';
import 'package:yike_mobile_app/Widgets/sent_msg.dart';

abstract class ListItem{}

class Sent extends ListItem{
  final String time,msg;
  Sent({this.msg,this.time});

}

class Recived extends ListItem{
  final String time,msg;
  Recived({this.msg,this.time});
}


class ChatPage extends StatelessWidget {
  List items=<ListItem>[
    Recived(msg: "Hello . How may i Help you ?", time: "10:21",),
    Sent(msg:"yesterday I registered a complaint about my Redgear Controller.So when are you going to resolve it",time:"10:22"),
    Recived(msg:"Sorry for inconvince But We aleready processed your Request and technician will come to your house within next four hours",time: "10:22",),
    Sent(msg: "0k",time: "10:23",)
  ];
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      appBar: AppBar(
        leading: Padding(padding: EdgeInsets.all(8.0),
        child:CircleAvatar(backgroundColor: Colors.white,minRadius: 20,),),
      title:Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Text("Red Gear Pvt. Ltd.", style: TextStyle(color: Colors.white,fontSize: 16),),
          Text("Sai Pranay raju",style:TextStyle(fontSize: 12,color: Colors.white))
        ],) ,
      ),
      body: ListView.builder(
        itemCount: items.length,
        itemBuilder: (context, index) {
            final item = items[index];
            if(item is Sent){
                return SendMessage(msg: item.msg,time: item.time,);
            }
            else{
              return RecivedMessage(msg: item.msg, time: item.time,);
            }
        }
      ),
      bottomNavigationBar: ChatPageFooter(),
    );
  }
}
