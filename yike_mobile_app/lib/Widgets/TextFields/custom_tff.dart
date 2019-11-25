import 'package:flutter/material.dart';

class CustomTextFormField extends StatefulWidget {
  final String label, hint, val;
  final TextEditingController controlleR;
  CustomTextFormField({
    this.label,
    this.hint,
    this.val,
    this.controlleR
  });

  @override
  State<StatefulWidget> createState() {
    // TODO: implement createState
    return _CustomTFFState();
  }
}

class _CustomTFFState extends State<CustomTextFormField> {
  String _label, _hint,_val;
  FocusNode _node;
  bool _focused = false;
  TextEditingController myController;

  @override
  void initState() {
    super.initState();
    myController = widget.controlleR;
    _label = widget.label;
    _hint = widget.hint;
    _val = widget.val;
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
  void dispose() {
    myController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return TextFormField(
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
      onChanged: (text) {
        
          setState(() {
            _val = text ;
          });
        
      },
      decoration: InputDecoration(
          focusedBorder: OutlineInputBorder(
            borderSide: BorderSide(color: Colors.blueAccent, width: 2.0),
          ),
          enabledBorder: OutlineInputBorder(
            borderSide: BorderSide(color: Colors.black38, width: 1.0),
          ),
          labelText: _focused ? _label :(_val.length==0?_hint:_label)),
    );
  }
}
