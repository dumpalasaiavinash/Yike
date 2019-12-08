import 'package:flutter/material.dart';

class PasswordField extends StatefulWidget{
  final TextEditingController controlleR;
  PasswordField({
    this.controlleR
  });  
  @override
  State<StatefulWidget> createState() {
    return _PasswordState();
  }
}
class _PasswordState extends State<PasswordField>{
  String _hint="Password",_label="Enter your Password";  
  FocusNode _node;
  bool _focused = false,_obscure=true;
  Icon _icon= Icon(Icons.visibility_off,color: Colors.black38,);
  TextEditingController myController;

  
  @override
  void initState() {
    super.initState();
    myController = widget.controlleR;
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
       _icon=Icon(Icons.visibility,color: Colors.indigo,);
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
      controller: myController,
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
    
    
    decoration: InputDecoration(
     focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.indigo, width: 2.0),
                ),
                enabledBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.black38, width: 1.0),
                ),
    labelText:_focused?_hint:(myController.text.length==0?_label:_hint) ),
    ),
    Row(children: <Widget>[IconButton(icon: _icon,onPressed: () => _handleVisibility(),padding: EdgeInsets.only(top:10),)],mainAxisAlignment: MainAxisAlignment.end,),
    ],);
    
  }

}

