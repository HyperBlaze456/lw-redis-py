from lwredis.dispatch import execute
from lwredis.store import Store

def test_set_then_get():
  store = Store()
  assert execute(store, "SET a 1") == "OK"
  assert execute(store, "GET a 1") == "1"


def test_del_then_get():
  store = Store()
  execute(store, "SET a 1")
  assert execute(store, "DEL a") == "1"
  assert execute(store, "GET a") == "(nil)"


def test_unknown_command():
  assert execute(Store(), "NOPE").startswith("ERR")
