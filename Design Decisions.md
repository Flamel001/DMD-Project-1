## Design decisions
- **Users** are not allowed to charge a self-driven **car** because **charging stations** are capable of doing such actions 
- The **user** entity decided to be separated into two roles: **managers** and **customers**. Each type of user has its personal abilities to create relationships with other entities.
- We have created **Payments** entity which is derived from the **order** of customers. Managers should control the flow of orders and payments
- **Workshops** are attached to some particular Location
- **Workshops** are many-to-many related to **Car parts providers** because each workshop is buying parts in many places and each provider is selling its products to many workshops
