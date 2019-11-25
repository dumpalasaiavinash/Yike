import 'package:flutter/material.dart';

class Password extends StatefulWidget{
  
  @override
  State<StatefulWidget> createState() {
    return _PasswordState();
  }
}
class _PasswordState extends State<Password>{
  String _hint="Password",_label="Enter your Password",_password="";  
  FocusNode _node;
  bool _focused = false,_obscure=true;
  Icon _icon= Icon(Icons.visibility_off,color: Colors.black38,);
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

  void _handleVisibility(){
    if(_obscure){
      setState(() {
       _obscure=false;
       _icon=Icon(Icons.visibility,color: Colors.blueAccent,);
      });
    }
    else{
      setState(() {
       _obscure=true;
       _icon=Icon(Icons.visibility_off,color: Colors.black38,); 
      });
    }

  }
  
  @override
  Widget build(BuildContext context) {

    
      
    return Stack(children: <Widget>[
      TextFormField(
      obscureText: _obscure,

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
        setState(() {
         _password=text;
        });
    },
    
    
    decoration: InputDecoration(
     focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.blueAccent, width: 2.0),
                ),
                enabledBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.black38, width: 1.0),
                ),
    labelText:_focused?_hint:(_password.length==0?_label:_hint) ),
    ),
    Row(children: <Widget>[IconButton(icon: _icon,onPressed: () => _handleVisibility(),padding: EdgeInsets.only(top:10),)],mainAxisAlignment: MainAxisAlignment.end,),
    ],);
    
  }

}

