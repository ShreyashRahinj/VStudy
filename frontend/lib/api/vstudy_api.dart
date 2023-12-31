import 'package:http/http.dart' as http;

class VStudyApi {
  Future<void> getRooms() async {
    try {
      final res = await http.get(
        Uri.parse('http://127.0.0.1:8000/api/rooms/'),
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
