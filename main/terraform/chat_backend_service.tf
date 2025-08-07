resource "kubernetes_service_v1" "chat_backend" {
  metadata {
    name      = "chat-backend"
    namespace = kubernetes_namespace_v1.chat.metadata[0].name
    labels    = { app = "chat-backend" }
  }

  spec {
    selector = { app = "chat-backend" }

    port {
      port        = 8000
      target_port = 8000
      protocol    = "TCP"
    }

    type = "ClusterIP"
  }
}
