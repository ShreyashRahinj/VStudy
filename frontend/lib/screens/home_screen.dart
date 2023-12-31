import 'package:flutter/material.dart';
import 'package:vstudy/api/vstudy_api.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: TextButton(
          onPressed: () {
            VStudyApi vStudyApi = VStudyApi();
            vStudyApi.getRooms();
          },
          child: const Text('Get Data'),
        ),
      ),
    );
  }
}
