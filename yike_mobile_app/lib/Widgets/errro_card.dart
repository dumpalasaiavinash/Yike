import 'package:flutter/material.dart';

class ErrorCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return  Card(
      color: Colors.white,
      child: Container(
        width: MediaQuery.of(context).size.width * 0.9,
        height: MediaQuery.of(context).size.height * 0.9,

      ),
    );
  }
}
