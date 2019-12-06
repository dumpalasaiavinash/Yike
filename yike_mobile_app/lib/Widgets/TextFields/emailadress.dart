import 'package:flutter/material.dart';

class EmailAddress extends StatefulWidget{
  
  @override
  State<StatefulWidget> createState() {
    return _EmailAddress();
  }
}
class _EmailAddress extends State<EmailAddress>{
  String _hint="Email Address",_label="Enter your Email Address",_email="";  
  FocusNode _node;
  bool _focused = false;
  @override
  void initState() {
    super.initState();
    _node = FocusNode(debugLabel: 'Button');
    _node.addListener(_handleFocusChange);
  }

  void _handleFocusChange() {
    if (_node.hasFocus != _focused) {
      setState(() {
        _focused = _node.hasFocus;
      });
    }
  }

  @override
  Widget build(BuildContext context) {

    
      
    return TextFormField(

      focusNode: _node,
      autofocus: false,
   onTap: () {
        print(_focused);
        if (_focused) {
          _node.unfocus();
        } else {
          _node.requestFocus();
        }
      },

    onChanged: (text){
      if(text.length==0){
        setState(() {
         _label=_hint; 
        });
      }
    },
    
    
    decoration: InputDecoration(
   
     focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.blueAccent, width: 2.0),
                ),
                enabledBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.black38, width: 1.0),
                ),
    labelText:_focused?_hint:_label ),);
  }
  

}

