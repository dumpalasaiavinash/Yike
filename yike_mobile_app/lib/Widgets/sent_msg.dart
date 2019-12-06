import "package:flutter/material.dart";

class SendMessage extends StatelessWidget {
  String str =
      "Hello. sorry for inconvenience. We will try to resolve your issue within next 5 hours";
  final msg, time;
  SendMessage({this.msg, this.time});
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Row(
      mainAxisAlignment: MainAxisAlignment.end,
      children: <Widget>[
        Expanded(
          flex: 3,
          child: Text(""),
        ),
        Expanded(
          flex: 8,
          child: Wrap(
            alignment: WrapAlignment.end,
            children: <Widget>[
              Container(
                margin: EdgeInsets.only(top: 16, left: 16, right: 16),
                padding: EdgeInsets.all(8),
                decoration: BoxDecoration(
                    boxShadow: [
                      BoxShadow(
                        color: Colors.grey[500],
                        offset: Offset(0.0, 1.5),
                        blurRadius: 1.5,
                      ),
                    ],
                    color: Colors.white,
                    borderRadius: BorderRadius.only(
                      topLeft: Radius.circular(16),
                      bottomLeft: Radius.circular(16),
                      bottomRight: Radius.circular(16),
                    )),
                child: Column(
                  children: <Widget>[
                    Text(
                      msg,
                      style: TextStyle(color: Colors.black54, fontSize: 14),
                    ),
                    Container(
                      width: msg.length * 7.toDouble() < 27
                          ? 27
                          : msg.length * 7.toDouble(),
                      margin: EdgeInsets.only(top: 4),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: <Widget>[
                          Text(
                            time,
                            style:
                                TextStyle(color: Colors.black54, fontSize: 10),
                          )
                        ],
                      ),
                    )
                  ],
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.start,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
