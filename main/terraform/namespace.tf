resource "kubernetes_namespace_v1" "chat" {
  metadata {
    name = "chat"
  }
}
