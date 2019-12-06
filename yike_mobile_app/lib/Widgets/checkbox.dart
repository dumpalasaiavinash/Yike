import 'package:flutter/material.dart';

class YikeCheckBox extends StatefulWidget{
  @override
  State<StatefulWidget> createState() {
    // TODO: implement createState
    return _YikeCheckBoxState();
  }
  
}

class _YikeCheckBoxState extends State<YikeCheckBox>{
  bool _resp = false;
  @override
  Widget build(BuildContext context) {
    return Checkbox(onChanged: (resp){
      setState(() {
       _resp=resp; 
      });
    },
    value: _resp,
    );
  }
}