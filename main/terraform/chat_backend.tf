resource "kubernetes_deployment_v1" "chat_backend" {
  metadata {
    name      = "chat-backend"
    namespace = kubernetes_namespace_v1.chat.metadata[0].name
    labels    = { app = "chat-backend" }
  }

  spec {
    replicas = 1
    selector {
      match_labels = { app = "chat-backend" }
    }

    template {
      metadata {
        labels = { app = "chat-backend" }
      }

      spec {
        container {
          name  = "api"
          image = "ghcr.io/mic2233/chat-backend:latest"
          port {
            container_port = 8000
          }
          env {
            name  = "SMTP_HOST"
            value = "mailhog-smtp.chat.svc.cluster.local"
          }
          env {
            name  = "SMTP_PORT"
            value = "1025"
          }
        }
      }
    }
  }
}
