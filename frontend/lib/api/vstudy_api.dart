import 'package:http/http.dart' as http;

class VStudyApi {
  void getRooms() async {
    try {
      final res = await http.get(
        Uri.parse('http://192.168.216.218:8000/api/rooms/'),
        headers: {
          'Content-Type': 'application/json',
        },
      );
      if (res.statusCode == 200) {
        print(res.body);
      }
    } on Exception catch (e) {
      print(e);
    }
  }
}
