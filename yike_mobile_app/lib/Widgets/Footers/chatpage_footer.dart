import 'package:flutter/material.dart';

class ChatPageFooter extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Container(
      padding: EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.grey[500],
            offset: Offset(0.0, 1.5),
            blurRadius: 1.5,
          ),
        ],
      ),
      child: Row(
        children: <Widget>[
          Expanded(
            flex: 8,
            child: TextFormField(
              decoration: InputDecoration(
                hintText: "Enter Your Message",
                enabledBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.black38, width: 1.0),
                ),
              ),
            ),
          ),
          Expanded(
            flex: 1,
            child: IconButton(
              onPressed: () {},
              icon: Icon(Icons.attach_file),
            ),
          ),
          Expanded(
            flex: 1,
            child: IconButton(
              onPressed: () {},
              icon: Icon(Icons.send),
            ),
          ),
        ],
      ),
    ); //Row(children: <Widget>[],);
  }
}
